export const errorMiddleware = (
    err,
    req,
    res,
    next
) => {
    return res.status(
        err.status || 500
    ).json({
        success: false,
        message: err.message ||
            'Internal server error',
        code: err.code ||
            'INTERNAL_SERVER_ERROR'
    });
};